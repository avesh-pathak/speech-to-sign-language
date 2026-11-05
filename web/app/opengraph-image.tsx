import { readFileSync } from "node:fs";
import { join } from "node:path";
import { ImageResponse } from "next/og";

export const alt = "VaniSign — Telugu speech to Indian Sign Language";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

const mark = `data:image/png;base64,${readFileSync(
  join(process.cwd(), "public/vanisign-icon.png")
).toString("base64")}`;

export default function OpengraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          background: "#FDFCFC",
          padding: "72px",
          fontFamily: "sans-serif",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "14px" }}>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={mark} width={54} height={54} alt="" />
          <div
            style={{
              fontSize: "34px",
              fontWeight: 600,
              letterSpacing: "-1px",
              color: "#100703",
            }}
          >
            VaniSign
          </div>
        </div>

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            fontSize: "72px",
            fontWeight: 400,
            lineHeight: 1.04,
            letterSpacing: "-2.4px",
            color: "#100703",
          }}
        >
          <span>Telugu speech in.</span>
          <span style={{ color: "#B83200" }}>Indian Sign Language out.</span>
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            gap: "24px",
            fontSize: "21px",
            color: "#6F6962",
          }}
        >
          <span>Telugu speech to Indian Sign Language</span>
          <span>github.com/avesh-pathak/speech-to-sign-language</span>
        </div>
      </div>
    ),
    { ...size }
  );
}
