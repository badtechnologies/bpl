import path from "path";
import fs from "fs";
import Fuse from "fuse.js";
import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  let query = new URLSearchParams(req.url.split("?")[1]).get("query");

  try {
    const files = fs.readdirSync(path.join(process.cwd(), "lib"), {
      withFileTypes: true,
    });

    const packages = files
      .filter((file) => file.isDirectory())
      .map((file) => file.name);

    if (!query) return NextResponse.json(packages);

    const fuse = new Fuse(packages);
    const results = fuse.search(query);

    const matchedPackages = results.map((result) => result.item);

    return NextResponse.json(matchedPackages);
  } catch {
    return NextResponse.json(
      { error: "Something went wrong" },
      { status: 500 }
    );
  }
}
