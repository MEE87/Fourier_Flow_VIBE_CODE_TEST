# FourierFlow: Interactive Fourier Transform Visualization

FourierFlow is a comprehensive educational web application designed to help users intuitively understand the Fourier Transform, from its geometric foundations to modern algorithmic implementations like the Fast Fourier Transform (FFT).

The application combines interactive visualizations, a structured 8-lesson course, and a creative "Studio" mode where users can draw or upload images to see them reconstructed using epicycles (Fourier Series).

## Features

### 1. Home Page: Harmonic Visualization
*   **Interactive Wave Synthesis**: Visualize how simple sine waves (harmonics) sum up to create complex waveforms like Square, Sawtooth, and Triangle waves.
*   **Real-time Controls**: Adjust the number of harmonics ($N$) and see the approximation improve in real-time.

### 2. Knowledge Base: The 8-Lesson Journey
A complete, self-contained course on Fourier Analysis covering:
*   **Lesson 1**: Geometry of Functions & Orthogonality.
*   **Lesson 2**: From Taylor to Fourier Series.
*   **Lesson 3**: Continuous Fourier Transform (CFT).
*   **Lesson 4**: Convolution Theorem & LTI Systems.
*   **Lesson 5**: Energy Conservation (Parseval's Theorem) & Distributions.
*   **Lesson 6**: Sampling Theorem & Aliasing.
*   **Lesson 7**: Discrete Fourier Transform (DFT) & FFT.
*   **Lesson 8**: Uncertainty Principle & Wavelets.
*   **Interactive Features**: Flip cards for summaries, modal windows for detailed lessons, and hidden "spoiler" answers for practice problems.
*   **Math Rendering**: High-quality LaTeX rendering via MathJax.

### 3. Studio Mode: The Epicycle Engine
*   **Draw to Fourier**: Draw any continuous path on the canvas, and the system computes the Discrete Fourier Transform (DFT) to reconstruct your drawing using rotating vectors (epicycles).
*   **Image to Vector**: Upload any image to convert it into a vector path using a built-in Canny Edge Detection pipeline (Grayscale -> Sobel Gradients -> Non-Maximum Suppression -> Hysteresis -> Greedy Stitching).
*   **3D "Vibe" Mode**: A playful 3D visualization where the canvas floats and reacts to microphone audio input (bass frequencies), creating a "dancing" effect.
*   **Export**: Save your generated Fourier art as a PNG image.

## Setup & Usage

Since this is a client-side web application with no backend dependencies, setup is extremely simple.

### Prerequisites
*   A modern web browser (Chrome, Firefox, Safari, Edge).
*   (Optional) A local web server for better performance, though opening the file directly often works.

### Running the Application

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd fourier-flow
    ```

2.  **Serve the application**:
    It is recommended to use a simple HTTP server to avoid CORS issues (especially for image processing features).

    *   **Using Python 3**:
        ```bash
        python3 -m http.server 8000
        ```
    *   **Using Node.js (http-server)**:
        ```bash
        npx http-server .
        ```

3.  **Open in Browser**:
    Navigate to `http://localhost:8000` in your web browser.

## Code Structure

The entire application logic is contained within `index.html` for simplicity and portability.

*   **HTML/CSS**: Uses Tailwind CSS (via CDN) for styling and standard HTML5 Canvas for rendering.
*   **JavaScript**:
    *   **State Management**: `state` object holds the global application state.
    *   **Math Engine**: Custom implementation of DFT (`dft` function) and geometric calculations.
    *   **Image Processing**: A raw JavaScript implementation of the Canny Edge Detection algorithm inside `processImage`.
    *   **Visualization**: `drawWaveLoop` (Home) and `drawStudioLoop` (Studio) handle the `requestAnimationFrame` render cycles.

## Dependencies

*   [Tailwind CSS](https://tailwindcss.com/): For utility-first styling (CDN).
*   [MathJax](https://www.mathjax.org/): For rendering LaTeX mathematical equations (CDN).

## License

[MIT License](LICENSE)
