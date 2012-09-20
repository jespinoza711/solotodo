var milliseconds_in_day = 86400000;

function create_chart() {
    new Highcharts.Chart({
        chart: {
            renderTo: 'chart_container',
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
        yAxis: [{
            title: {
                text: null
            },
            min: 0
        }, {
            title: {
                text: null
            },
            min: 0,
            opposite: true
        }],
        tooltip: {
            formatter: function() {
                return Highcharts.dateFormat('%d de %B de %Y', this.x) + ': <b>' + Highcharts.numberFormat(this.y, 0, ',', '.') + '</b>';
            }
        },
        series: chart_data,

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
            resetZoom: 'Reiniciar zoom'
        }
    });

    if ($('ul.errorlist').length == 0) {
        create_chart();
    }
});