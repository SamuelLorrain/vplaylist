<script lang="ts">
    import { invalidateAll } from '$app/navigation';
    import { onMount } from 'svelte';
    import type { PageData } from './$types';
    export let data : PageData;
    let videoElement;
    let number: int = 0;

    const plus = () => (number >= data.length) ? '' : number += 1;
    const minus = () => number <= 0 ? '' : number -= 1;
    const fetchPlaylist = () => {
        invalidateAll();
    }

    $: current = data.playlist[number];
    $: videoSrc = `http://localhost:8000/video/${current.uuid}`;

    onMount(() => {
        videoElement.addEventListener("ended", () => {
            number += 1;
        });
    })
</script>

<section>
    <h1>Player</h1>
    <video bind:this={videoElement} controls src={videoSrc} width="500" autoplay>
    </video>
    <button on:click={minus}>-</button>
    <button on:click={plus}>+</button>
    <button on:click={fetchPlaylist}>Another playlist</button>
    {#each data.playlist as video (video.uuid)}
    <div>
        {#if video.uuid === current.uuid}
            <div><b>{video.path}</b></div>
        {:else}
            <div>{video.path}</div>
        {/if}
    </div>
    {/each}
</section>
