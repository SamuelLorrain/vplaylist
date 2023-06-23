'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  DropdownMenu,
  DropdownMenuLabel,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useSWRConfig } from 'swr';
import { useGetNewPlaylistUrl } from '@/hooks/videoDetails';
import { searchOptions, globalKeydownEventIsCancelled } from '@/contexts/recoilState';
import { useSetRecoilState } from 'recoil';

export default function Home() {
  const fetchUrl = useGetNewPlaylistUrl();
  const { mutate } = useSWRConfig();
  const [searchValue, setSearchValue] = useState('');
  const [noWebmValue, setNoWebmValue] = useState(false);
  const [qualityValue, setQualityValue] = useState('all');
  const [lastValue, setLastValue] = useState(false);
  const [bestValue, setBestValue] = useState(false);
  const setFetchContext = useSetRecoilState(searchOptions);
  const setGlobalKeydownEventIsCancelledState = useSetRecoilState(globalKeydownEventIsCancelled);

  // trigger re-fetch
  function updateContext() {
    setFetchContext({
        fetchingOptions: {
            noWebm: noWebmValue,
            quality: qualityValue,
            last: lastValue,
            best: bestValue,
        },
        search: searchValue
    });
  }

  return (
    <div className="flex py-5 px-10 justify-center items-center border-b-2 sticky top-0 mb-5 bg-white z-50">
        <div className="flex gap-2">
            <Button variant="secondary"
                    className="whitespace-nowrap"
                    onClick={() => mutate(fetchUrl.toString())}
            >
                Another playlist
            </Button>
            <Input type="text"
                   placeholder="search"
                   value={searchValue}
                   onChange={(e) => setSearchValue(e.target.value)}
                   onFocus={() => {
                    setGlobalKeydownEventIsCancelledState(true);
                   }}
                   onBlur={() => {
                        setGlobalKeydownEventIsCancelledState(false)
                   }}
            />
            <Button onClick={_ => updateContext()}>Search</Button>
            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <Button className="whitespace-nowrap">Search options</Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                    <DropdownMenuLabel>
                        Quality
                    </DropdownMenuLabel>
                    <DropdownMenuRadioGroup value={qualityValue}
                                            onValueChange={(e) => setQualityValue(e)}>
                        <DropdownMenuRadioItem value="all">
                            All
                        </DropdownMenuRadioItem>
                        <DropdownMenuRadioItem value="sd">
                            SD
                        </DropdownMenuRadioItem>
                        <DropdownMenuRadioItem value="hd">
                            HD
                        </DropdownMenuRadioItem>
                    </DropdownMenuRadioGroup>
                    <DropdownMenuLabel>
                        Format
                    </DropdownMenuLabel>
                    <DropdownMenuCheckboxItem checked={noWebmValue}
                                              onCheckedChange={e => setNoWebmValue(e)}>
                        No Webm
                    </DropdownMenuCheckboxItem>
                    <DropdownMenuLabel>
                        Preferences
                    </DropdownMenuLabel>
                    <DropdownMenuCheckboxItem checked={lastValue}
                                              onCheckedChange={e => setLastValue(e)}>
                        Last
                    </DropdownMenuCheckboxItem>
                    <DropdownMenuCheckboxItem checked={bestValue}
                                              onCheckedChange={e => setBestValue(e)}>
                        Best
                    </DropdownMenuCheckboxItem>
                </DropdownMenuContent>
            </DropdownMenu>
        </div>
    </div>
  )
}
