$(document).ready(function() {
    $('.source').select2({
        width: '100%',
        minimumInputLength: 2,
        ajax: {
            url: 'search_source',
            dataType: 'json',
            delay: 250,
            data: function(params) {
                var query = {
                    search: params.term
                }
                return query;
            },
            processResults: function(data) {
                console.log(data)
                return {
                    results: data.results
                }
            },
            cache: true
        },
        templateResult: formatRepo,
        templateSelection: formatRepoSelection
    });

    $('.user').select2({
        width: '100%',
        minimumInputLength: 2,
        ajax: {
            url: 'search_user',
            dataType: 'json',
            delay: 250,
            data: function(params) {
                var query = {
                    search: params.term
                }
                return query;
            },
            processResults: function(data) {
                console.log(data)
                return {
                    results: data.results
                }
            },
            cache: true
        },
        templateResult: formatRepo,
        templateSelection: formatRepoSelection
    });

    function formatRepo(repo) {
        if (repo.loading) return repo.text;

        var $container = $(
            "<div class='select2-result-repository clearfix'>" +
              "<div class='select2-result-repository__meta'>" +
                "<div class='select2-result-repository__title'></div>" +
                "<div class='select2-result-repository__description'></div>" +
              "</div>" +
            "</div>"
        );

          $container.find(".select2-result-repository__title").text(repo.title);
          $container.find(".select2-result-repository__description").text(repo.description);

        return $container;
    };

    function formatRepoSelection (repo) {
        return repo.selection_text || repo.text;
    };
});

