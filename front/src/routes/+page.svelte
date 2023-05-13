<script lang="ts">
    import type { PageData } from './$types';
    export let data : PageData;
    let number: int = 0;
    const plus = () => (number >= data.length) ? '' : number += 1;
    const minus = () => number <= 0 ? '' : number -= 1;
    $: current = data.playlist[number];
    $: videoSrc = `http://localhost:8000/video/${current.uuid}`;
</script>

<section>
    <h1>Player</h1>
    <video controls src={videoSrc} width="500" autoplay>
    </video>
    <button on:click={minus}>-</button>
    <button on:click={plus}>+</button>
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
