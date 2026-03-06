# Ad-page

A modern web application for earning points by watching advertisements, built with Next.js and integrated with Vercel Speed Insights.

## Features

- 🚀 Built with Next.js 14 (App Router)
- ⚡ Integrated Vercel Speed Insights for performance monitoring
- 💰 Points-based earning system
- 🎨 Modern, responsive UI with Tailwind CSS
- 📊 Real-time performance tracking with Speed Insights

## Getting Started

### Prerequisites

- Node.js 18+ installed
- A Vercel account for deployment

### Installation

1. Install dependencies:

```bash
npm install
```

2. Run the development server:

```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Building for Production

```bash
npm run build
npm start
```

## Vercel Speed Insights

This project has Vercel Speed Insights integrated to monitor and optimize performance metrics including:

- Core Web Vitals (LCP, FID, CLS)
- Time to First Byte (TTFB)
- First Contentful Paint (FCP)
- Interaction to Next Paint (INP)

### How Speed Insights is Implemented

The Speed Insights component is integrated in the root layout (`app/layout.tsx`):

```tsx
import { SpeedInsights } from '@vercel/speed-insights/next'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <SpeedInsights />
      </body>
    </html>
  )
}
```

### Viewing Speed Insights Data

After deploying to Vercel:

1. Go to your [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Navigate to the **Speed Insights** tab
4. View real-time performance metrics from actual users

## Deployment to Vercel

### Option 1: Using Vercel CLI

```bash
npm i -g vercel
vercel deploy
```

### Option 2: Connect Git Repository

1. Push your code to GitHub/GitLab/Bitbucket
2. Visit [vercel.com/new](https://vercel.com/new)
3. Import your repository
4. Vercel will automatically detect Next.js and configure the build

### Enabling Speed Insights

1. In your Vercel project dashboard, click on the **Speed Insights** tab
2. Click **Enable** to activate Speed Insights
3. Deploy your application
4. Speed Insights will automatically start collecting data

> **Note:** Speed Insights routes are available at `/_vercel/speed-insights/*` after deployment.

## Project Structure

```
ad-page/
├── app/
│   ├── layout.tsx          # Root layout with Speed Insights
│   ├── page.tsx            # Home page
│   └── globals.css         # Global styles
├── public/                 # Static assets
├── Bot.py                  # Telegram bot for ad viewing
├── package.json
├── tsconfig.json
└── next.config.js
```

## Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS (via globals.css)
- **Analytics:** Vercel Speed Insights
- **Bot:** Python Telegram Bot

## Related Projects

This web application works in conjunction with a Telegram bot (`Bot.py`) that allows users to:
- Watch advertisements
- Earn points
- Track earnings
- Request withdrawals

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Vercel Speed Insights Documentation](https://vercel.com/docs/speed-insights)
- [Deploy to Vercel](https://vercel.com/docs/deployments/overview)

## License

MIT
