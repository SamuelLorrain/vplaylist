import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load = (async () => {
    let playlist;
    const response = await fetch('http://127.0.0.1:8000/playlist/create')
    const content = await response.json()
    return {
       playlist: content.playlist
    }
}) satisfies PageLoad;
