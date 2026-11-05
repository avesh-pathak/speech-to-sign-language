const vercelHost =
  process.env.VERCEL_PROJECT_PRODUCTION_URL ?? process.env.VERCEL_URL;

export const siteUrl = new URL(
  process.env.NEXT_PUBLIC_SITE_URL ??
    (vercelHost ? `https://${vercelHost}` : "http://localhost:3000")
);

export const siteConfig = {
  name: "VaniSign",
  title: "VaniSign — Telugu speech to Indian Sign Language",
  description:
    "VaniSign is a speech-to-sign translation framework for Telugu. It recognises spoken Telugu, produces an ordered ISL gloss sequence, and plays the matching sign frames — with a text fallback that never drops a word.",
  author: {
    name: "Avesh Pathak",
    github: "https://github.com/avesh-pathak",
    linkedin: "https://www.linkedin.com/in/avesh-pathak/",
    portfolio: "https://avesh.tech",
  },
} as const;
