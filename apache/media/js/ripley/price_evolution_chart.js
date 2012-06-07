var milliseconds_in_day = 86400000;
var series;
var chart;

function round_to_day(millis, func) {
    return func(millis / milliseconds_in_day) * milliseconds_in_day;
}

function create_chart() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'detail-container',
            reflow: false,
            zoomType: 'x'
        },
        credits: {
            enabled: false
        },
        title: {
            text: null
        },
        xAxis: {
            type: 'datetime',
            minRange: milliseconds_in_day,
            maxZoom: milliseconds_in_day,
            dateTimeLabelFormats: {
                hour: ' '
            }
        },
        yAxis: {
            title: {
                text: null
            },
        },
        tooltip: {
            formatter: function() {
                return Highcharts.dateFormat('%d de %B de %Y', this.x) + '<br /><b>$' + Highcharts.numberFormat(this.y, 0, ',', '.') + '</b>';
            }
        },
        series: series,

        exporting: {
            enabled: false
        }

    });
}

$(function() {
    Highcharts.setOptions({
        lang: {
            months: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiempre', 'Octubre', 'Noviembre',
                'Diciembre'],
            shortMonths: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul',
                'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            resetZoom: 'Reiniciar zoom',
        }
    });

    $('a.chart_link').click(function (e) {
        console.log("chart!");

        $.getJSON('json', function(json_data) {
            series = json_data;
            create_chart();
        });
    })
});