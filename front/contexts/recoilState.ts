import { atom } from 'recoil';

export const playlist = atom({
    key: 'playlist',
    default: [],
})

export const currentPlaylistElement = atom({
    key: 'currentPlaylistElement',
    default: {
        idx: -1,
        uuid: '',
    }
})

export const searchOptions = atom({
    key: 'searchOptions',
    default: {
        fetchingOptions: {
            noWebm: false,
            quality: 'all',
            last: false,
            best: false,
        },
        search: '',
    }
});

export const openVideoDetails = atom({
    key: 'openVideoDetails',
    default: false,
})
