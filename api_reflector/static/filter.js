active_tags = [];

function find_ancestor(el, cls) {
    while ((el = el.parentElement) && !el.classList.contains(cls));
    return el;
}

function toggle_tag(button) {
    if (button.classList.contains('btn-secondary')) {
        // button is currently inactive, so activate it
        button.classList.remove('btn-secondary');
        button.classList.add('btn-primary');

        // add the tag to the active_tags array
        active_tags.push(button.id);
    } else {
        // button is currently active, so deactivate it
        button.classList.remove('btn-primary');
        button.classList.add('btn-secondary');

        // remove the tag from the active_tags array
        active_tags.splice(active_tags.indexOf(button.id), 1);
    }

    update_list_items();
}

function update_list_items() {
    if (active_tags.length == 0) {
        // no tags are active, so show all endpoint cards
        document.querySelectorAll('div.endpoint.card').forEach(function (item) {
            item.classList.remove('d-none');
        });

        // also show all response items
        document.querySelectorAll('.response-list-item').forEach(function (item) {
            item.classList.remove('d-none');
        });

        return;
    }

    // get all list items
    var list_items = document.getElementsByClassName('response-list-item');

    // list of all parent cards, and cards to show
    var all_cards = new Set();
    var show_cards = new Set();

    // loop through all list items
    for (var i = 0; i < list_items.length; i++) {
        // get the current list item
        var response_item = list_items[i];

        // get the list item's tags
        var tags = response_item.getElementsByClassName('tag');

        // get the parent card div
        var parent_card = find_ancestor(response_item, 'card');

        // check if any of the list item's tags are in active_tags
        var show = false;
        for (var j = 0; j < tags.length; j++) {
            if (active_tags.includes(tags[j].id)) {
                show = true;
                break;
            }
        }

        // show/hide the response item
        if (show) {
            response_item.classList.remove('d-none');
        } else {
            response_item.classList.add('d-none');
        }

        // track the parents to hide and show
        all_cards.add(parent_card);
        if (show) {
            show_cards.add(parent_card);
        }
    }

    // show & hide cards
    all_cards.forEach(function (card) {
        if (show_cards.has(card)) {
            card.classList.remove('d-none');
        } else {
            card.classList.add('d-none');
        }
    });
}
