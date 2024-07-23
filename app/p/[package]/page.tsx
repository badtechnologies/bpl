import path from "path";
import fs from "fs";
import { notFound } from "next/navigation";
import { PackageInfo } from "@/types/package";
import { Snippet } from "@nextui-org/snippet";
import { Link } from "@nextui-org/link";

export default function Page({ params }: { params: { package: string } }) {
  const fp = path.join(process.cwd(), "..", "lib", params.package, "bpl.json");
  if (!fs.existsSync(fp)) {
    notFound();
  }
  const info: PackageInfo = JSON.parse(fs.readFileSync(fp, "utf-8"));

  return (
    <div className="p-5 container mx-auto">
      <div className="border-default-300 border-b-1 pb-4 mb-4 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-semibold">{info.name}</h1>
          <p className="text-default-500">
            {params.package} • {info.version} • {info.author}
          </p>
        </div>
        <Snippet>{"bpm install " + params.package}</Snippet>
      </div>

      <div className="space-y-4">
        {info.requires && (
          <div>
            <h2 className="text-xl font-semibold">Dependencies</h2>
            {info.requires?.map((p, i) => (
              <Link showAnchorIcon underline="hover" href={`/p/${p}`} key={i}>
                {p}
              </Link>
            ))}
          </div>
        )}

        <div>
          <h2 className="text-xl font-semibold">License</h2>
          <p>{info.license ? info.license : "MIT"}</p>
        </div>

        {info.homepage && (
          <div>
            <h2 className="text-xl font-semibold">Homepage</h2>
            <Link
              isExternal
              showAnchorIcon
              underline="hover"
              href={info.homepage}
            >
              {info.homepage.split("://")[1]}
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
