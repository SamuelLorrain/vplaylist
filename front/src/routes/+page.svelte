<script lang="ts">
    import { invalidateAll } from '$app/navigation';
    import { onMount } from 'svelte';
    import VideoPlayer from '../components/VideoPlayer.svelte';
    import Playlist from '../components/Playlist.svelte';
    import Toolbar from '../components/Toolbar.svelte';
    import VideoDetails from '../components/VideoDetails.svelte';
    import type { PageData } from './$types';
    export let data : PageData;
    let number = 0;
    const plus = () => (number >= data.length) ? '' : number += 1;
    const minus = () => number <= 0 ? '' : number -= 1;
    const fetchPlaylist = () => {
        invalidateAll();
        number = 0;
    }
    $: current = data.playlist[number] || undefined;
    $: videoSrc = `http://127.0.0.1:8000/video/${current.uuid}`;
    $: formattedName = current?.path.split('/')[current?.path.split('/').length-1]
</script>

<Toolbar fetchPlaylist={fetchPlaylist}/>
<!-- <div class="container flex gap-1 mt-2"> -->
<!--     <div class="w-3/4"> -->
<!--         <VideoPlayer -->
<!--             src={videoSrc} -->
<!--             currentVideo={current} -->
<!--             endVideoCallback={plus} -->
<!--             nextVideoCallback={plus} -->
<!--             previousVideoCallback={minus} -->
<!--             errorVideoCallback={plus} /> -->
<!--         <VideoDetails title={formattedName} videoData={current}/> -->
<!--     </div> -->
<!--     <div class="w-1/4"> -->
<!--         <Playlist -->
<!--             collection={data.playlist} -->
<!--             currentVideo={current} -->
<!--             clickOnVideoCallback={(i) => number = i}/> -->
<!--     </div> -->
<!-- </div> -->
