import { NextResponse } from "next/server";
import { project } from "@/lib/project";

export async function GET() {
  return NextResponse.json(
    {
      ok: true,
      project,
    },
    {
      headers: {
        "Cache-Control": "public, s-maxage=3600, stale-while-revalidate=86400",
      },
    }
  );
}
