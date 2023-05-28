<script>
export let data;
</script>

<div>
    <ul>
        <li>name: {data.name ?? ''}</li>
        <li>date_down: {data.date_down && new Date(data.date_down)}</li>
        <li>width : {data.width}</li>
        <li>height: {data.height}</li>
    </ul>
    <div>
        Tags:
        <ul>
            {#each data.tags as tag }
                <li>{tag.name}</li>
            {/each}
        </ul>
    </div>
    <div>
        Participant:
        <ul>
          {#each data.participants as participant }
             <li>
             {participant.name}
             |
             {#each participant.tags as tag}
               {tag.name}&nbsp;
             {/each}
             </li>
          {/each}
        </ul>
    </div>
</div>
