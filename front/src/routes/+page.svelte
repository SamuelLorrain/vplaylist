<script lang="ts">
    import { invalidateAll } from '$app/navigation';
    import { onMount } from 'svelte';
    import VideoPlayer from './VideoPlayer.svelte';
    import Playlist from './Playlist.svelte';
    import Toolbar from './Toolbar.svelte';
    import VideoDetails from './VideoDetails.svelte';
    import type { PageData } from './$types';
    export let data : PageData;
    let number = 0;
    const plus = () => (number >= data.length) ? '' : number += 1;
    const minus = () => number <= 0 ? '' : number -= 1;
    const fetchPlaylist = () => {
        invalidateAll();
        number = 0;
    }
    $: current = data.playlist[number];
    $: videoSrc = `http://127.0.0.1:8000/video/${current.uuid}`;

    // todo dynamic height for video player ?
</script>

<section class="layout">
    <div class="video-section">
        <VideoPlayer src={videoSrc}
                     currentVideo={current}
                     endVideoCallback={plus}
                     nextVideoCallback={plus}
                     previousVideoCallback={minus}
                     errorVideoCallback={plus}
        />
        <Toolbar fetchPlaylist={fetchPlaylist}/>
    </div>
    <div>
        <Playlist
            collection={data.playlist}
            currentVideo={current}
            clickOnVideoCallback={(i) => number = i}/>
        <VideoDetails videoData={current}/>
    </div>
</section>

<style>
.layout {
    display: flex;
    height: 98vh;
    overflow-y: hidden;
    box-sizing: border-box;
}
</style>
