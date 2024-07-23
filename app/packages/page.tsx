"use client";

import { PackageListing } from "@/components/package-listing";
import { useSearchParams } from "next/navigation";
import React, { useEffect, useState } from "react";

export default function Page() {
  let query = useSearchParams().get("q");
  let params = query ? `?query=${query}` : "";

  const [packages, setPackages] = useState<[] | null>(null);

  useEffect(() => {
    const fetchPackages = async () => {
      try {
        const response = await fetch(`/api/packages${params}`);
        const data = await response.json();
        setPackages(data);
      } catch {}
    };

    fetchPackages();
  }, []);

  return (
    <div className="p-5 container px-20 mx-auto">
      <h1 className="text-2xl font-semibold">
        {query ? `Search results for "${query}"` : "All packages"}
      </h1>
      {packages ? (
        <>
          <p className="text-default-500">{packages.length} packages found</p>
          <ul>
            {packages.map((pkg, index) => (
              <li key={index}>
                <PackageListing pkg={pkg} />
              </li>
            ))}
          </ul>
        </>
      ) : (
        <p className="text-default-500">Looking for packages...</p>
      )}
    </div>
  );
}
