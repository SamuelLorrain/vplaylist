'use client';

import React, { useContext, useState } from 'react';
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
import { PlaylistContext } from '@/contexts/PlaylistContext';
import { useGetNewPlaylistUrl } from '@/hooks/videoDetails';

export default function Home() {
  const fetchUrl = useGetNewPlaylistUrl();
  const { fetchingOptions, setFetchingOptions, setSearch } = useContext(PlaylistContext);
  const { mutate } = useSWRConfig();
  const [searchValue, setSearchValue] = useState('');

  return (
    <div className="flex py-5 px-10 justify-center items-center border-b-2 sticky top-0 mb-5 bg-white z-50">
        <div className="flex gap-2">
            <Button variant="secondary" className="whitespace-nowrap" onClick={() => mutate(fetchUrl.toString())}>
                Another playlist
            </Button>
            <Input type="text" placeholder="search" value={searchValue} onChange={(e) => setSearchValue(e.target.value)}/>
            <Button onClick={_ => setSearch(searchValue)}>Search</Button>
            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <Button className="whitespace-nowrap">Search options</Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                    <DropdownMenuLabel>
                        Quality
                    </DropdownMenuLabel>
                    <DropdownMenuRadioGroup value={fetchingOptions.quality}
                                            onValueChange={e => setFetchingOptions({quality: e, noWebm: fetchingOptions.noWebm, last: fetchingOptions.last, best:fetchingOptions.best})}>
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
                    <DropdownMenuCheckboxItem checked={fetchingOptions.noWebm}
                                              onCheckedChange={e => setFetchingOptions({noWebm: e, quality: fetchingOptions.quality, last: fetchingOptions.last, best: fetchingOptions.best})}>
                        No Webm
                    </DropdownMenuCheckboxItem>
                    <DropdownMenuLabel>
                        Preferences
                    </DropdownMenuLabel>
                    <DropdownMenuCheckboxItem checked={fetchingOptions.last}
                                              onCheckedChange={e => setFetchingOptions({quality: fetchingOptions.quality, noWebm: fetchingOptions.noWebm, last: e, best: fetchingOptions.best})}>
                        Last
                    </DropdownMenuCheckboxItem>
                    <DropdownMenuCheckboxItem checked={fetchingOptions.best}
                                            onCheckedChange={e => setFetchingOptions(
                                                {quality: fetchingOptions.quality, noWebm: fetchingOptions.noWebm, last: fetchingOptions.last, best: e}
                                                )}>
                        Best
                    </DropdownMenuCheckboxItem>
                </DropdownMenuContent>
            </DropdownMenu>
        </div>
    </div>
  )
}
