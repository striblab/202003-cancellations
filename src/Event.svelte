<script>
  export let event;
  let category_labels = {
    'arts': 'Arts',
    'business': 'Business',
    'concert': 'Concert',
    'free': 'Free services',
    'gov': 'Government',
    'grocery': 'Grocery Store',
    'pharm': 'Pharmacy',
    'religious': 'Religious',
    'restaurant': 'Restaurants',
    'sports': 'Sports',
    'other': 'Other events',
    'all': 'All'
  }
</script>

<div class="eventCard">
  <h5 class="title-{event.category}">{category_labels[event.category]}</h5>
  <h3>{event.event_name}</h3>
  <p class="city">
    {#if event.status == "Open"}
      {#if event.venue}
        {event.venue} - <span class="open">{event.status}</span>
      {:else}
        {event.city} - <span class="open">{event.status}</span>
      {/if}
    {:else if event.status == "Other"}
      {#if event.venue}
        {event.venue} - {event.status}
      {:else}
        {event.city} - {event.status}
      {/if}
    {:else}
      {#if event.venue}
        {event.venue} - <span class="closed">{event.status}</span>
      {:else}
        {event.city} - <span class="closed">{event.status}</span>
      {/if}
  {/if}
  </p>
  <p>{event.desc}</p>
</div>
