"use client";

import { Button } from "@nextui-org/button";
import { Input } from "@nextui-org/input";
import { MagnifyingGlass } from "@phosphor-icons/react";
import React, { useState } from "react";

type SearchProps = {
  isFeature?: boolean;
};

export const Search: React.FC<SearchProps> = ({ isFeature }) => {
  const [value, setValue] = useState("");

  function search() {
    window.location.href = `/packages?q=${encodeURIComponent(value)}`;
  }

  const handleKeyDown = (event: {
    key: string;
    preventDefault: () => void;
  }) => {
    if (event.key === "Enter") {
      event.preventDefault();
      search();
    }
  };

  if (isFeature) {
    return (
      <div className="flex w-full gap-2">
        <Input
          aria-label="Search"
          classNames={{
            label: "text-black/50 dark:text-white/90",
            input: [
              "bg-transparent",
              "text-black/90 dark:text-white/90",
              "placeholder:text-default-700/60 dark:placeholder:text-white/60",
            ],
            innerWrapper: "bg-transparent",
            inputWrapper: [
              "shadow-xl",
              "bg-default-200/50",
              "dark:bg-default/60",
              "backdrop-blur-xl",
              "backdrop-saturate-200",
              "hover:bg-default-200/70",
              "dark:hover:bg-default/70",
              "group-data-[focus=true]:bg-default-200/50",
              "dark:group-data-[focus=true]:bg-default/60",
              "!cursor-text",
            ],
          }}
          className="max-w-[512px]"
          labelPlacement="outside"
          placeholder="Search the BadOS Package Portal..."
          startContent={<MagnifyingGlass className="text-default-600/60" />}
          type="search"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
        />

        <Button color="primary" onPress={() => search()}>
          Search
        </Button>
      </div>
    );
  } else {
    return (
      <Input
        aria-label="Search"
        classNames={{
          inputWrapper: "bg-default-100 border border-default-300",
          input: "text-ellipsis",
        }}
        className="w-full"
        labelPlacement="outside"
        placeholder="Search the BadOS Package Portal..."
        startContent={<MagnifyingGlass className="text-default-600/60" />}
        type="search"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
      />
    );
  }
};
