## Packages
framer-motion | Smooth transitions and layout animations
recharts | Visualizing signal scores and authority metrics
react-markdown | Rendering the generated blog post content
lucide-react | Icons for the dashboard UI
clsx | Utility for constructing className strings conditionally
tailwind-merge | Utility for merging Tailwind classes efficiently

## Notes
The application is a single-page dashboard where users input a keyword.
The pipeline process might take some time, so we need a robust loading state.
The response data is complex and nested; we need to carefully visualize each section (Signals, Strategy, Blog, Social).
Status logic:
- If `halt` is true, stop rendering and show the reason.
- If `authority_approved` is true, enable social sharing features.
