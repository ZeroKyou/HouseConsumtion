
var chart;

function requestData() {
    $.ajax({
        url: '/meter/electricity/year/values/',
        success: function(data) {
            if ((typeof data != undefined) && (data.current != undefined) && (data.current.length > 0)) {
                $('.show-avg-data').toggle(true);
                $('.show-no-avg-data').toggle(false);
                $('#avg_c').html(data['avg_c']);
                $('#avg_v').html(data['avg_v']);
                $('#avg_p').html(data['avg_p']);
                $('#cost').html(data['cost'] + '€');
            }
            else{
                $('.show-avg-data').toggle(false);
                $('.show-no-avg-data').toggle(true);
            }

            // add the point
            chart.series[0].setData(data['current']);
            chart.series[1].setData(data['voltage']);
            chart.series[2].setData(data['power']);

            // call it again after one second
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
            text: "Consumo do último ano"
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
                    text += "<strong>" + this.x + "</strong><br />";
                    text += this.y + "A";
                }
                else if(this.series.name == 'Tensão') {
                    text += "<strong>" + this.x + "</strong><br />";
                    text += this.y + "V";
                }
                if(this.series.name == 'Potência') {
                    text += "<strong>" + this.x + "</strong><br />";
                    text += this.y + "W";
                }
                return text;
            }
        },
        xAxis: {
            categories: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
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