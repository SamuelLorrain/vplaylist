<script>
    import { onMount } from 'svelte';
    export let fetchPlaylist;
    let best = false;
    let last = false;
    let search = "";
    let noWebm = false;
    let quality = "all";
    let shift = 0;

    onMount(() => {
        best = (new URL(window.location).searchParams.get('best') === 'true') || false;
        last = (new URL(window.location).searchParams.get('last') === 'true') || false;
        noWebm  = (new URL(window.location).searchParams.get('no_webm') === 'true') || false;
        quality = new URL(window.location).searchParams.get('quality') || 'all';
        search = new URL(window.location).searchParams.get('search') || '';
        shift = new URL(window.location).searchParams.get('shift') || 0;
    })

    const handleChange = (e) => {
        const url = new URL(window.location)
        url.searchParams.set('best', best);
        url.searchParams.set('last', last);
        url.searchParams.set('search', search);
        url.searchParams.set('no_webm', noWebm);
        url.searchParams.set('quality', quality)
        url.searchParams.set('shift', shift);
        window.history.replaceState(null, undefined, url);
        fetchPlaylist();
    }

    const reset = () => {
        best = false;
        last = false;
        search = "";
        noWebm = false;
        quality = "all";
        shift = 0;
        handleChange();
    }
</script>

<div>
    <button on:click={fetchPlaylist}>Another playlist</button>
    <input class="checkbox" type="checkbox" bind:checked={best} on:change={handleChange}>
    <input class="checkbox" type="checkbox" bind:checked={last} on:change={handleChange}>
    <input class="checkbox" type="checkbox" bind:checked={noWebm} on:change={handleChange}>
    <select class="select" bind:value={quality} on:change={handleChange}>
        <option value="all">All</option>
        <option value="hd">HD</option>
        <option value="sd">SD</option>
    </select>
    <input type="text" bind:value={search}>
    <button on:click={handleChange}>Search</button>
    <button on:click={reset}>Reset</button>
</div>
