"use client";

import { Search } from "@/components/search";
import { siteConfig } from "@/config/site";
import { Link } from "@nextui-org/link";
import { Snippet } from "@nextui-org/snippet";

export default function Home() {
  return (
    <div>
      <section className="bg-gradient-to-br from-emerald-300 to-sky-400 dark:from-emerald-500 dark:to-sky-600 py-16">
        <div className="text-center items-center flex flex-col container mx-auto gap-12">
          <h1 className="text-4xl">
            Explore BadOS packages with the{" "}
            <span className="font-semibold">Package Portal</span>
          </h1>

          <div className="flex sm:w-[512px] gap-2">
            <Search isFeature />
          </div>

          <p>
            Or,{" "}
            <Link
              href="/packages"
              color="foreground"
              underline="hover"
              className="font-semibold"
            >
              browse all packages
            </Link>
            .
          </p>
        </div>
      </section>

      <section className="max-w-[64rem] mx-auto space-y-4 py-8">
        <h1 className="text-2xl font-semibold">
          What is the BadOS Package Portal?
        </h1>
        <p>
          The BadOS Package Portal is an online application to index and browse
          the BadOS Dynamic Shell Package Library (BPL). The BPL contains a
          library of software for BDSH, shared by first-party developers and the
          community.
        </p>
        <p>
          The creation, publication, etc. of BadOS packages is documented{" "}
          <Link
            href={siteConfig.links.docs.bpl}
            color="foreground"
            underline="always"
            className="font-semibold"
            isExternal
          >
            here
          </Link>
          .
        </p>
      </section>

      <section className="max-w-[64rem] mx-auto space-y-4 py-8">
        <h1 className="text-2xl font-semibold">
          Package Management (installation, removal, etc.)
        </h1>
        <p>
          To download, install, remove, or otherwise manage your packages, use
          the BadOS Package Manager (BPM) tool.
        </p>
        <p>
          All installations of BDSH should have the latest version of BPM. If
          you don&apos;t, setup the system again, or manually download it if
          you&apos;re up to it.
        </p>
        <div className="space-y-1">
          <p className="text-sm text-default-600">Install a package</p>
          <Snippet size="sm">bpm install &lt;package name&gt;</Snippet>
        </div>
        <div className="space-y-1">
          <p className="text-sm text-default-600">Uninstall a package</p>
          <Snippet size="sm">bpm remove &lt;package name&gt;</Snippet>
        </div>
      </section>
    </div>
  );
}
