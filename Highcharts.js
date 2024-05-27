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

    buildLineChart('container-1', TEMP_TIME_SERIES.batiment1.piece1.capteur1.donnees, 'Température', 'Température (°C)', TEMP_TIME_SERIES.batiment1.piece1.loc);
    buildLineChart('container-2', NOISE_TIME_SERIES.batiment1.piece1.capteur1.donnees, 'Niveau sonore', 'Niveau sonore (dB)', NOISE_TIME_SERIES.batiment1.piece1.loc);
    buildMultiLineChart('container-3', GAZ_TIME_SERIES.batiment1.piece1.capteur1.donnees, GAZ_TIME_SERIES.batiment1.piece1.loc);

    document.getElementById('Piece1').addEventListener('click', function() {
        document.getElementById('container-1').innerHTML = '';
        document.getElementById('container-2').innerHTML = '';
        document.getElementById('container-3').innerHTML = '';

        buildLineChart('container-1', TEMP_TIME_SERIES.batiment1.piece1.capteur1.donnees, 'Température', 'Température (°C)', TEMP_TIME_SERIES.batiment1.piece1.loc);
        buildLineChart('container-2', NOISE_TIME_SERIES.batiment1.piece1.capteur1.donnees, 'Niveau sonore', 'Niveau sonore (dB)', NOISE_TIME_SERIES.batiment1.piece1.loc);
        buildMultiLineChart('container-3', GAZ_TIME_SERIES.batiment1.piece1.capteur1.donnees, GAZ_TIME_SERIES.batiment1.piece1.loc);
    });

    document.getElementById('Couloir').addEventListener('click', function() {
        document.getElementById('container-1').innerHTML = '';
        buildLineChart('container-1', TEMP_TIME_SERIES.batiment1.couloir.capteur1.donnees, 'Température', 'Température (°C)', TEMP_TIME_SERIES.batiment1.couloir.loc);
    });

    document.getElementById('Exterieur').addEventListener('click', function() {
        document.getElementById('container-1').innerHTML = '';
        buildLineChart('container-1', TEMP_TIME_SERIES.exterieur.capteur1.donnees, 'Température', 'Température (°C)', TEMP_TIME_SERIES.exterieur.loc);
    });

    document.getElementById('Piece2').addEventListener('click', function() {
        document.getElementById('container-1').innerHTML = '';
        document.getElementById('container-2').innerHTML = '';
        document.getElementById('container-3').innerHTML = '';

        buildLineChart('container-1', TEMP_TIME_SERIES.batiment1.piece2.capteur1.donnees, 'Température', 'Température (°C)', TEMP_TIME_SERIES.batiment1.piece2.loc);
        buildLineChart('container-2', NOISE_TIME_SERIES.batiment1.piece2.capteur1.donnees, 'Niveau sonore', 'Niveau sonore (dB)', NOISE_TIME_SERIES.batiment1.piece2.loc);
        buildMultiLineChart('container-3', GAZ_TIME_SERIES.batiment1.piece2.capteur1.donnees, GAZ_TIME_SERIES.batiment1.piece2.loc);
    });
});
