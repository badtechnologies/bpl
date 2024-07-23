import { Button } from "@nextui-org/button";
import { ArrowRight, Package } from "@phosphor-icons/react";
import Link from "next/link";
import React from "react";

type PackageListingProps = {
  pkg: string;
};

export const PackageListing: React.FC<PackageListingProps> = ({ pkg }) => (
  <Link
    href={`/p/${pkg}`}
    className="rounded-xl bg-default-50 p-2 my-4 flex items-center justify-between max-w-96"
  >
    <div className="flex items-center space-x-2">
      <Package weight="fill" size={22} />
      <h2>{pkg}</h2>
    </div>
    <Button color="primary" isIconOnly size="sm">
      <ArrowRight size={18} />
    </Button>
  </Link>
);
