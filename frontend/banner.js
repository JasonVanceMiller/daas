function search_func() {
    // this would send to a long results page
    return;
}
function ai_search_func() {
    // this would send to a long results page
    return;
}

// this would be fetched from opensearch after ~5 characters are typed in the search bar 
const documents=["alpha", "beta", "gamma", "kappa", "omega"];

function update_search_preview_func() {
    const searchbar = document.getElementById("searchbar_id");
    if (searchbar.value === '') {
        // searchbar is empty. Clear the results
        document.getElementById('search_preview_list_id').innerHTML = '';
        return;
    }

    // build the list of previewed results
    const ul = document.createElement('ul');
    for (let i = 0; i < documents.length; i++) {
        if (documents[i].indexOf(searchbar.value) != -1) {

            const li = document.createElement('li');
            const a = document.createElement('a');

            a.href = documents[i] + ".html"; // @TODO this should be a more nuanced doc id system.
            a.textContent = documents[i];

            li.appendChild(a);
            ul.appendChild(li);

        }
    }

    // clear the old list and replace it 
    document.getElementById('search_preview_list_id').innerHTML = '';
    document.getElementById('search_preview_list_id').appendChild(ul);
}
