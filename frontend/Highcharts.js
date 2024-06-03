function buildLineChart(container, graphData, graph_title, unite, loc) {
    Highcharts.chart(container, {
        chart: {
            type: 'line'
        },
        title: {
            text: graph_title
        },
        subtitle: {
            text: loc
        },
        xAxis: {
            type: 'datetime',
            title: {
                text: 'Date'
            }
        },
        yAxis: {
            title: {
                text: unite
            }
        },
        legend: {
            enabled: false
        },
        credits: {
            enabled: false
        },
        series: graphData
    });
}

function buildMultiLineChart(container, graphData, loc) {
    Highcharts.chart(container, {
        chart: {
            type: 'line'
        },
        title: {
            text: 'Concentration de gaz'
        },
        subtitle: {
            text: loc
        },
        xAxis: {
            type: 'datetime',
            title: {
                text: 'Date'
            }
        },
        yAxis: {
            title: {
                text: 'Concentration (ppm)'
            }
        },
        credits: {
            enabled: false
        },
        series: graphData
    });
}

document.addEventListener('DOMContentLoaded', function() {
    Highcharts.setOptions({
        global: {
            useUTC: false
        },
        lang: {
            loading: 'Chargement...',
            months: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
            weekdays: ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'],
            shortMonths: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jui', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'],
            thousandsSep: " ",
            decimalPoint: ','
        }
    });
});
