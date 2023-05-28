<script>
import { modalStore } from '@skeletonlabs/skeleton';
export let videoDetails;

console.log(videoDetails);

const closeModal = () => {
    modalStore.close();
}
</script>

<div class="card">
    <div class="card-header">
        <h3 class="h3">Edit video details</h3>
    </div>
    <form class="px-4 mb-4">
        <label class="label">
            <span>Name</span>
            <input class="input" type="text"/>
        </label>
        <label class="label">
            <span>Date down</span>
            <input class="input" type="date"/>
        </label>
    </form>
    <div class="card-footer flex justify-end gap-3">
        <button class="btn variant-ghost" on:click={closeModal}>Cancel</button>
        <button class="btn variant-filled">Submit</button>
    </div>
</div>
