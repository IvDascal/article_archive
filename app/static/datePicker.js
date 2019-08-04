$(document).ready(function() {
    $('.date-single-picker').daterangepicker({
        singleDatePicker: true,
        timePicker: true,
        timePicker24Hour: true,
        alwaysShowCalendars: true,

        locale: {
          format: 'YYYY-MM-DD HH:mm:SS'
        }
    });

    $('input.date-range-picker').daterangepicker({
        timePicker: true,
        timePicker24Hour: true,
        alwaysShowCalendars: true,
        autoUpdateInput: false,
        locale: {
          format: 'DD.MM.YYYY HH:mm'
        }
    });

    $('input.date-range-picker').on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('DD.MM.YYYY HH:mm') + ' - ' + picker.endDate.format('DD.MM.YYYY HH:mm'));
    });

    $('input.date-range-picker').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    });


});

