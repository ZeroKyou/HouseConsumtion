
var chart;

function requestData() {
    $.ajax({
        url: '/meter/electricity/actual/values/',
        success: function(data) {
            var series = chart.series[0],
                shift = series.data.length > 20; // shift if the series is longer than 20

            if ((typeof data != undefined) && (data.current != undefined) && (data.current.length > 0)) {
                $('.show-avg-data').toggle(true);
                $('.show-no-avg-data').toggle(false);
                $('#avg_c').html(data['avg_c']);
                $('#avg_v').html(data['avg_v']);
                $('#avg_p').html(data['avg_p']);
                $('#cost').html(data['cost'] + '€');
                chart.legend.group.show();
                chart.legend.box.show();
                chart.legend.display = true;
            }
            else{
                $('.show-avg-data').toggle(false);
                $('.show-no-avg-data').toggle(true);
                chart.legend.group.hide();
                chart.legend.box.hide();
                chart.legend.display = false;
            }

            // Add points
            chart.series[0].setData(data['current']);
            chart.series[1].setData(data['voltage']);
            chart.series[2].setData(data['power']);

            // Call it again every one second
            setTimeout(requestData, 1000);
        },
        cache: false
    });
}

$(document).ready(function() {
    Highcharts.setOptions({
        lang: {noData: "Não existem dados a apresentar :("},
        global: {
            timezoneOffset: -60
        }
    });

    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'graph-container',
            defaultSeriesType: 'column',
            events: {
                load: requestData
            }
        },
        title: {
            text: "Consumo do último minuto"
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -70,
            y: 30,
            floating: true,
            backgroundColor: '#ffffff',
            borderWidth: 1
        },
        tooltip: {
            shared: false,
            formatter: function(){
                var text = '';
                if(this.series.name == 'Corrente') {
                    var options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
                    date = new Date(this.x);
                    text = "<strong>"+date.getHours()+"h"+date.getMinutes()+"m"+date.getSeconds()+"s</strong><br />";
                    text += this.y + "A";
                }
                else if(this.series.name == 'Tensão') {
                    var options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
                    date = new Date(this.x);
                    text = "<strong>Hora: "+date.getHours()+"h"+date.getMinutes()+"m"+date.getSeconds()+"s</strong><br />";
                    text += this.y + "V";
                }
                if(this.series.name == 'Potência') {
                    var options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
                    date = new Date(this.x);
                    text = "<strong>Hora: "+date.getHours()+"h"+date.getMinutes()+"m"+date.getSeconds()+"s</strong><br />";
                    text += this.y + "W";
                }
                return text;
            }
        },
        xAxis: {
            type: 'datetime',
            tickInterval: 5 * 1000, // every 5 seconds
            labels: {
                format: '{value:%H:%M:%S}'
            }
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            type: 'logarithmic',
            title: {
                text: 'Valores',
            }
        },
        series: [
            {
                name: 'Corrente',
                data: []
            },
            {
                name: 'Tensão',
                data: []
            },
            {
                name: 'Potência',
                data: []
            },
        ]
    });
    chart.legend.group.hide();
    chart.legend.box.hide();
    chart.legend.display = false;
});