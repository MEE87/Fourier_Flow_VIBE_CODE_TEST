import os

css_insert = """
        /* Mobile Navigation */
        @media (max-width: 768px) {
            nav {
                padding: 1rem !important; /* px-4 py-4 */
                flex-direction: column;
                gap: 1rem;
            }
            nav > div:first-child {
                margin-bottom: 0.5rem;
            }
            nav > div:last-child {
                gap: 1rem !important; /* Smaller gap between items */
                padding: 0.5rem 1rem !important;
                width: 100%;
                justify-content: center;
            }
        }
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

if "/* Mobile Navigation */" not in content:
    content = content.replace("/* Mobile Studio Controls */", css_insert + "\n        /* Mobile Studio Controls */")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated CSS")
else:
    print("CSS already updated")
