"use client";

import { createContext } from 'react';

export type PlaylistDataType = {
    playlist: {
        uuid: string
    }[]
};

export type FetchingOptionsType = {
    noWebm: boolean,
    quality: string,
    last: boolean,
    best: boolean
};

export type PlaylistContextDataType = {
    currentUUID: string|null;
    data?: PlaylistDataType|null;
    fetchingOptions: FetchingOptionsType;
    setCurrentUUID: Function,
    setData: Function,
    setFetchingOptions: Function,
    search?: string,
    setSearch: Function
};

export const PlaylistContext = createContext<PlaylistContextDataType>({
    currentUUID: null,
    data: null,
    fetchingOptions: {
        noWebm: false,
        quality: 'all',
        last: false,
        best: false
    },
    setData: () => null,
    setCurrentUUID: () => null,
    setFetchingOptions: () => null,
    setSearch: () => null,
});
