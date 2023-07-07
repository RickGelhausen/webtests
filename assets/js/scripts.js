---
---


document.addEventListener("DOMContentLoaded", function() {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.navbar ul');
    if (burger && nav) {
        burger.addEventListener('click', function() {
            nav.classList.toggle('nav-open');
        });
    } else {
        console.warn('burger or nav elements not found!');
    }

    function updatePublications() {
        var search_query = $('#search-bar').val().toLowerCase();
        var filter_year = $('#year-filter').val();
        var filter_author = $('#author-filter').val().toLowerCase();

        $('#reset-year-filter').toggle(!!filter_year);
        $('#reset-author-filter').toggle(!!filter_author);

        $('.publication').each(function() {
            var content = $(this).text().toLowerCase();
            var year = $(this).attr('data-year');
            var authors = $(this).attr('data-author').split(';').map(author => author.trim().toLowerCase());
            var matches_search = !search_query || content.includes(search_query);
            var matches_filter = !filter_year || year == filter_year;
            var matches_author = !filter_author || authors.includes(filter_author);

            $(this).toggle(matches_search && matches_filter && matches_author);
        });

        var visible_count = $('.publication:visible').length;
        $('#publication-count').text(visible_count + " publication(s) found!");
    }

    $('#reset-year-filter').click(function() {
        $('#year-filter').prop('selectedIndex', 0);
        updatePublications();
        document.getElementById('publications').scrollTop = 0;
    });

    $('#reset-author-filter').click(function() {
        $('#author-filter').val('');
        updatePublications();
        document.getElementById('publications').scrollTop = 0;
    });

    $('#search-bar, #year-filter, #author-filter').on('input change', updatePublications);

    var years = {};
    $('.publication').each(function() {
        var year = $(this).attr('data-year');
        years[year] = (years[year] || 0) + 1;
    });
    var year_filter = $('#year-filter');
    year_filter.append('<option value="">All years</option>');
    Object.keys(years).sort().reverse().forEach(function(year) {
        year_filter.append('<option value="' + year + '">' + year + ' (' + years[year] + ')' + '</option>');
    });

    updatePublications();
});