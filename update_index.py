import os

try:
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace DFT with FFT
    dft_block = """        // --- Same logic as V7.0 below ---
// --- DFT Algorithm ---
        function dft(x) {
            const X = [];
            const N = x.length;
            for (let k = 0; k < N; k++) {
                let re = 0;
                let im = 0;
                for (let n = 0; n < N; n++) {
                    const phi = (2 * Math.PI * k * n) / N;
                    re += x[n].x * Math.cos(phi) + x[n].y * Math.sin(phi);
                    im += x[n].y * Math.cos(phi) - x[n].x * Math.sin(phi);
                }
                re = re / N;
                im = im / N;

                let freq = k;
                let amp = Math.sqrt(re * re + im * im);
                let phase = Math.atan2(im, re);

                // Handle negative frequencies
                if (k > N / 2) {
                    freq = k - N;
                }

                X[k] = { re, im, freq, amp, phase };
            }
            return X;
        }"""

    fft_block = """        // --- Same logic as V7.0 below ---
// --- FFT Algorithm ---
        class Complex {
            constructor(re, im) {
                this.re = re;
                this.im = im;
            }
            add(c) { return new Complex(this.re + c.re, this.im + c.im); }
            sub(c) { return new Complex(this.re - c.re, this.im - c.im); }
            mult(c) { return new Complex(this.re * c.re - this.im * c.im, this.re * c.im + this.im * c.re); }
        }

        function fft(x) {
            const N = x.length;
            if (N <= 1) return x;

            const even = [];
            const odd = [];
            for (let i = 0; i < N; i++) {
                if (i % 2 === 0) even.push(x[i]);
                else odd.push(x[i]);
            }

            const evenFFT = fft(even);
            const oddFFT = fft(odd);

            const X = new Array(N);
            for (let k = 0; k < N / 2; k++) {
                const angle = -2 * Math.PI * k / N;
                const W = new Complex(Math.cos(angle), Math.sin(angle));
                const t = W.mult(oddFFT[k]);

                X[k] = evenFFT[k].add(t);
                X[k + N / 2] = evenFFT[k].sub(t);
            }
            return X;
        }

        function resamplePath(path, N) {
            if (path.length === 0) return [];

            // Calculate total length
            let totalDist = 0;
            const dists = []; // Store cumulative distances
            dists.push(0);

            for (let i = 0; i < path.length - 1; i++) {
                const dx = path[i+1].x - path[i].x;
                const dy = path[i+1].y - path[i].y;
                const d = Math.sqrt(dx*dx + dy*dy);
                totalDist += d;
                dists.push(totalDist);
            }

            // Handle single point case
            if (totalDist === 0) {
                const arr = [];
                for(let i=0; i<N; i++) arr.push(path[0]);
                return arr;
            }

            const step = totalDist / N;
            const newPath = [];

            // Interpolate
            let currentPathIdx = 0;
            for (let i = 0; i < N; i++) {
                const targetDist = i * step;

                // Find segment
                while (currentPathIdx < dists.length - 1 && dists[currentPathIdx+1] < targetDist) {
                    currentPathIdx++;
                }

                if (currentPathIdx >= path.length - 1) {
                    newPath.push(path[path.length - 1]);
                } else {
                    const startDist = dists[currentPathIdx];
                    const endDist = dists[currentPathIdx+1];
                    const segLen = endDist - startDist;

                    if (segLen === 0) {
                        newPath.push(path[currentPathIdx]);
                    } else {
                        const ratio = (targetDist - startDist) / segLen;
                        const p1 = path[currentPathIdx];
                        const p2 = path[currentPathIdx+1];
                        newPath.push({
                            x: p1.x + (p2.x - p1.x) * ratio,
                            y: p1.y + (p2.y - p1.y) * ratio
                        });
                    }
                }
            }
            return newPath;
        }"""

    if dft_block in content:
        content = content.replace(dft_block, fft_block)
    else:
        print("Error: DFT block not found")
        # Try to find partial match to debug
        if "function dft(x)" in content:
            print("function dft(x) found, but block mismatch.")
        else:
            print("function dft(x) not found.")
        exit(1)


    # 2. Replace calculateFourier
    calc_block = """        function calculateFourier(skip) {
            statusMsg.innerText = "Computing DFT...";
            const sampled = [];
            for(let i=0; i<state.path.length; i+=skip) sampled.push(state.path[i]);

            state.fourierX = dft(sampled);

            if (state.isImageMode) {
                state.fourierX[0].re = 0;
                state.fourierX[0].im = 0;
            }

            state.fourierX.sort((a, b) => b.amp - a.amp);
            state.drawTime = 0;
            state.lastPoint = null;
            statusMsg.innerText = `Drawing (${state.fourierX.length} cycles)`;
        }"""

    new_calc_block = """        function calculateFourier(skip) {
            statusMsg.innerText = "Computing FFT...";
            document.getElementById('loading-overlay').classList.add('active');

            // Allow UI to update before blocking
            setTimeout(() => {
                // 1. Resample to Power of 2
                let N = 256;
                const targetLen = state.path.length;
                // Adaptive resolution based on drawing complexity
                if (targetLen > 256) N = 512;
                if (targetLen > 512) N = 1024;
                if (targetLen > 1024) N = 2048;
                if (targetLen > 2048) N = 4096;
                // Cap at 4096 for performance

                const resampled = resamplePath(state.path, N);

                // 2. Convert to Complex
                const complexArray = resampled.map(p => new Complex(p.x, p.y));

                // 3. FFT
                const fftResult = fft(complexArray);

                // 4. Format Output
                state.fourierX = [];
                const len = fftResult.length;
                for (let k = 0; k < len; k++) {
                    let re = fftResult[k].re / len;
                    let im = fftResult[k].im / len;

                    let freq = k;
                    let amp = Math.sqrt(re * re + im * im);
                    let phase = Math.atan2(im, re);

                    // Handle negative frequencies
                    if (k > len / 2) {
                        freq = k - len;
                    }

                    state.fourierX.push({ re, im, freq, amp, phase });
                }

                if (state.isImageMode) {
                     const dc = state.fourierX.find(x => x.freq === 0);
                     if(dc) { dc.re = 0; dc.im = 0; dc.amp = 0; }
                }

                state.fourierX.sort((a, b) => b.amp - a.amp);
                state.drawTime = 0;
                state.lastPoint = null;
                statusMsg.innerText = `Drawing (${state.fourierX.length} cycles)`;
                document.getElementById('loading-overlay').classList.remove('active');
            }, 10);
        }"""

    if calc_block in content:
        content = content.replace(calc_block, new_calc_block)
    else:
        print("Error: calculateFourier block not found")
        exit(1)

    # 3. Add CSS for Loading Overlay and Mobile Controls
    style_block = """<style>
        /* Loading Overlay */
        #loading-overlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(5px);
            z-index: 200;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s;
        }
        #loading-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }
        .spinner {
            width: 50px; height: 50px;
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
            margin-bottom: 20px;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        /* Mobile Studio Controls */
        @media (max-width: 768px) {
            #studio-controls-panel {
                top: auto !important;
                bottom: 20px;
                right: 20px;
                width: calc(100% - 40px) !important;
                max-height: 40vh;
                overflow-y: auto;
            }
        }
    </style>"""
    content = content.replace("</head>", style_block + "\n</head>")

    # 4. Inject HTML for Loading Overlay
    html_insert = """
    <!-- Loading Overlay -->
    <div id="loading-overlay">
        <div class="spinner"></div>
        <div class="text-xs font-mono tracking-widest text-gray-400">PROCESSING FOURIER TRANSFORM</div>
    </div>
"""
    content = content.replace('<div id="lesson-modal">', html_insert + '\n    <div id="lesson-modal">')

    # 5. Add ID to Studio Panel
    studio_panel_start = '<div class="absolute top-24 right-8 glass-panel'
    studio_panel_replacement = '<div id="studio-controls-panel" class="absolute top-24 right-8 glass-panel'
    if studio_panel_start in content:
        content = content.replace(studio_panel_start, studio_panel_replacement)
    else:
        print("Warning: Studio panel not found for ID injection")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Success")

except Exception as e:
    print(e)
