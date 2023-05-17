<script lang="ts">
    import { invalidateAll } from '$app/navigation';
    import { onMount } from 'svelte';
    import type { PageData } from './$types';
    export let data : PageData;
    let videoElement;
    let number: int = 0;
    let best: bool = false;
    let last: bool = false;
    let search: str = "";
    let noWebm: bool = false;

    const plus = () => (number >= data.length) ? '' : number += 1;
    const minus = () => number <= 0 ? '' : number -= 1;
    const fetchPlaylist = () => {
        invalidateAll();
        number = 0;
    }
    const handleChange = (e) => {
        const url = new URL(window.location)
        url.searchParams.set('best', best);
        url.searchParams.set('last', last);
        url.searchParams.set('search', search);
        url.searchParams.set('no_webm', noWebm);
        window.history.replaceState(null, undefined, url);
        invalidateAll();
        number = 0;
    }
    const reset = () => {
        best = false;
        last = false;
        search = "";
        noWebm = false;
        invalidateAll();
    }
    $: current = data.playlist[number];
    $: videoSrc = `http://localhost:8000/video/${current.uuid}`;

    onMount(() => {
        videoElement.addEventListener("ended", plus);
        videoElement.addEventListener("error", plus);
        best = (new URL(window.location).searchParams.get('best') === 'true') || false;
        last = (new URL(window.location).searchParams.get('last') === 'true') || false;
        noWebm  = (new URL(window.location).searchParams.get('no_webm') === 'true') || false;
        search = new URL(window.location).searchParams.get('search') || '';

        window.addEventListener('keydown', (e) => {
        console.log(e);
            if (e.code === 'Space') {
                if (videoElement.paused) {
                    videoElement.play();
                } else {
                    videoElement.pause();
                }
            } else if (e.key === '>') {
                plus();
            } else if (e.key === '<') {
                minus();
            } else if (e.key === 'f') {
                videoElement.requestFullScreen();
            }
        });

        return () => {
            videoElement.removeEventListener("ended", plus);
            videoElement.removeEventListener("error", plus);
        }
    })
    // todo dynamic height for video player ?
</script>

<section class="layout">
    <div class="video-section">
        <div class="video-container">
            <video bind:this={videoElement} controls src={videoSrc} height="600" autoplay>
            </video>
        </div>
        <div class="video-title">{current.path}</div>
        <div class="toolbar">
            <button on:click={minus}>-</button>
            <button on:click={plus}>+</button>
            <button on:click={fetchPlaylist}>Another playlist</button>
            <label>
                <input type="checkbox" bind:checked={best} on:change={handleChange}>
                Best
            </label>
            <label>
                <input type="checkbox" bind:checked={last} on:change={handleChange}>
                Last
            </label>
            <label>
                <input type="checkbox" bind:checked={noWebm} on:change={handleChange}>
                No Webm
            </label>
            <label>
                <input type="text" bind:value={search}>
                <button on:click={handleChange}>Search</button>
            </label>
            <button on:click={reset}>Reset</button>
        </div>
    </div>
    <div class="playlist">
      {#each data.playlist as video, i (video.uuid)}
          <div class="playlist-element">
              {#if video.uuid === current.uuid}
                  <div><b>{video.path}</b></div>
              {:else}
                  <button on:click={() => number=i}>{video.path}</button>
              {/if}
          </div>
      {/each}
    </div>
</section>

<style>
.layout {
    display: grid;
    grid-template: 1fr / 2fr 1fr;
    height: 98vh;
    overflow-y: hidden;
    box-sizing: border-box;
}

.video-container {
    display:flex;
    justify-content:center;
    border: 1px solid black;
    background-color: black;
}

.video-title {
    text-align: center;
}

.toolbar {
    display: flex;
    gap: 10px;
    align-items: center;
}

.toolbar button {
    border: 1px solid black;
    border-radius: 2px;
    padding: 5px 10px;
    background: inherit;
    cursor: pointer;
}

.playlist {
    overflow-y: scroll;
}

.playlist button {
    border: 0;
    background: inherit;
    cursor: pointer;
    text-align: start;
}
</style>
