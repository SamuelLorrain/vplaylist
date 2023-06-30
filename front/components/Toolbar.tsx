'use client';

import React, { useState, useMemo, useEffect } from 'react';
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
import { Label } from './ui/label';
import { Checkbox } from "@/components/ui/checkbox"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

export default function Toolbar() {
  const fetchUrl = useGetNewPlaylistUrl();
  const { mutate } = useSWRConfig();
  const [searchValue, setSearchValue] = useState('');
  const [noWebmValue, setNoWebmValue] = useState(false);
  const [qualityValue, setQualityValue] = useState('all');
  const [lastValue, setLastValue] = useState(false);
  const [bestValue, setBestValue] = useState(false);
  const setFetchContext = useSetRecoilState(searchOptions);
  const setGlobalKeydownEventIsCancelledState = useSetRecoilState(globalKeydownEventIsCancelled);
  const [isMobile, setIsMobile] = useState(true);

  useEffect(() => {
    const listener = () => setIsMobile(window.matchMedia("(max-width: 768px)").matches);
    window.addEventListener('resize', listener);
    return () => window.removeEventListener('resize', listener);
   }, [setIsMobile])


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

  const mobileToolbar = useMemo(() => {
      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button className="whitespace-nowrap">Search options</Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent>
              <div className="flex flex-col gap-4">
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
                <Select onValueChange={(v) => setQualityValue(v)}>
                    <SelectTrigger>
                        <SelectValue placeholder="Quality" defaultValue="all"/>
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="all">All</SelectItem>
                        <SelectItem value="sd">SD</SelectItem>
                        <SelectItem value="hd">HD</SelectItem>
                    </SelectContent>
                </Select>
                <div className="flex gap-2 h-5 items-center">
                  <Checkbox id="no-webm" checked={noWebmValue} onCheckedChange={e => setNoWebmValue(Boolean(e.valueOf()))}/>
                  <Label htmlFor="no-webm">
                      No webm
                  </Label>
                </div>
                <div className="flex gap-2 h-5 items-center">
                  <Checkbox id="last" checked={lastValue} onCheckedChange={e => setLastValue(Boolean(e.valueOf()))}/>
                  <Label htmlFor="last">
                      Last
                  </Label>
                </div>
                <div className="flex gap-2 h-5 items-center">
                  <Checkbox id="best" checked={lastValue} onCheckedChange={e => setBestValue(Boolean(e.valueOf()))}/>
                  <Label htmlFor="best">
                      Last
                  </Label>
                </div>
              </div>
          </DropdownMenuContent>
        </DropdownMenu>
      );
  },[
    mutate,
    fetchUrl.toString(),
    searchValue,
    setSearchValue,
    setGlobalKeydownEventIsCancelledState,
    setGlobalKeydownEventIsCancelledState,
    updateContext,
    qualityValue,
    setQualityValue,
    noWebmValue,
    setNoWebmValue,
    lastValue,
    setLastValue,
    bestValue,
    setBestValue
   ]);

  const desktopToolbar = useMemo(() => {
      return (
          <>
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
          </>
      );
  },[
    mutate,
    fetchUrl.toString(),
    searchValue,
    setSearchValue,
    setGlobalKeydownEventIsCancelledState,
    setGlobalKeydownEventIsCancelledState,
    updateContext,
    qualityValue,
    setQualityValue,
    noWebmValue,
    setNoWebmValue,
    lastValue,
    setLastValue,
    bestValue,
    setBestValue
   ]);

  return (
    <div className="flex py-5 px-10 justify-start items-center border-b-2 sticky top-0 md:mb-5 bg-white z-50">
      <div className="text-2xl font-bold">
          Vplaylist
      </div>
      <div className={isMobile ? "flex ml-auto gap-3" : "flex mx-auto gap-3"}>
          {isMobile ? <>{mobileToolbar}</> : <>{desktopToolbar}</>}
      </div>
    </div>
  )
}
