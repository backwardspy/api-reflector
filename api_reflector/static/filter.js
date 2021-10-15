const INACTIVE_TAG_CLASS = 'btn-outline-primary';
const ACTIVE_TAG_CLASS = 'btn-primary';

let active_tags = [];

function find_ancestor(el, cls) {
    while ((el = el.parentElement) && !el.classList.contains(cls));
    return el;
}

function toggle_tag(button) {
    if (button.classList.contains(INACTIVE_TAG_CLASS)) {
        button.classList.remove(INACTIVE_TAG_CLASS);
        button.classList.add(ACTIVE_TAG_CLASS);

        // add the tag to the active_tags array
        active_tags.push(button.id);
    } else {
        button.classList.remove(ACTIVE_TAG_CLASS);
        button.classList.add(INACTIVE_TAG_CLASS);

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
        var tag_elements = response_item.getElementsByClassName('tag');
        var tags = Array.prototype.map.call(tag_elements, tag => tag.id);

        // get the parent card div
        var parent_card = find_ancestor(response_item, 'card');

        // check if all of the active tags are in the list item's tags
        var show = true;
        for (var j = 0; j < active_tags.length; j++) {
            if (!tags.includes(active_tags[j])) {
                show = false;
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
