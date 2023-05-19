<script>
    import { onMount } from 'svelte';
    export let fetchPlaylist;
    let best = false;
    let last = false;
    let search = "";
    let noWebm = false;

    onMount(() => {
        best = (new URL(window.location).searchParams.get('best') === 'true') || false;
        last = (new URL(window.location).searchParams.get('last') === 'true') || false;
        noWebm  = (new URL(window.location).searchParams.get('no_webm') === 'true') || false;
        search = new URL(window.location).searchParams.get('search') || '';
    })

    const handleChange = (e) => {
        const url = new URL(window.location)
        url.searchParams.set('best', best);
        url.searchParams.set('last', last);
        url.searchParams.set('search', search);
        url.searchParams.set('no_webm', noWebm);
        window.history.replaceState(null, undefined, url);
        fetchPlaylist();
    }

    const reset = () => {
        best = false;
        last = false;
        search = "";
        noWebm = false;
        handleChange();
    }
</script>

<div class="toolbar">
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

<style>
.toolbar {
    display: flex;
    gap: 20px;
    justify-content:center;
    align-items: center;
}

.toolbar button {
    border: 1px solid black;
    border-radius: 2px;
    padding: 5px 10px;
    background: inherit;
    cursor: pointer;
}
</style>
