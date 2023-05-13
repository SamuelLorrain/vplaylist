<script lang="ts">
    import type { PageData } from './$types';
    export let data : PageData;

    let number: int = 0;
    const plus = () => (number >= data.length) ? '' : number += 1;
    const minus = () => number <= 0 ? '' : number -= 1;
    $: double = number * 2;
</script>

<section>
    <h1>Player</h1>
    <button on:click={minus}>-</button>
    <button on:click={plus}>+</button>
    <div>{JSON.stringify(data.playlist[number])}</div>
</section>
