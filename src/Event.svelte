<script>
  export let event;
  let category_labels = {
    'arts': 'Arts',
    'business': 'Business',
    'concert': 'Concert',
    'gov': 'Government',
    'grocery': 'Grocery Store',
        'mall': 'Mall',
    'pharm': 'Pharmacy',
    'religious': 'Religious',
    'restaurant': 'Restaurant',
    'sports': 'Sports',
    'other': 'Other',
    'all': 'All'
  }
</script>

<div class="eventCard">
  <h5 class="title-{event.category}">{category_labels[event.category]}</h5>
  <h3>{event.event_name}</h3>
  <p class="city">
    {#if event.status == "Open"}
      {#if event.venue}
        {event.venue} <span class="bullet">&bull;</span> <span class="open">{event.status}</span>
      {:else}
        {event.city} <span class="bullet">&bull;</span> <span class="open">{event.status}</span>
      {/if}
    {:else if event.status == "Other"}
      {#if event.venue}
        {event.venue} <span class="bullet">&bull;</span> {event.status}
      {:else}
        {event.city} <span class="bullet">&bull;</span> {event.status}
      {/if}
    {:else}
      {#if event.venue}
        {event.venue} <span class="bullet">&bull;</span> <span class="closed">{event.status}</span>
      {:else}
        {event.city} <span class="bullet">&bull;</span> <span class="closed">{event.status}</span>
      {/if}
  {/if}
  </p>
  <p>{event.desc}</p>
  {#if event.url}
    <a class="eventUrl" href="{event.url}" target="_blank">Website</a>
  {/if}
</div>
