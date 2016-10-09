
var chart;

function requestData() {
    $.ajax({
        url: '/meter/water/month/values/',
        success: function(data) {
            if ((typeof data != undefined) && (data.day_l != undefined) && (data.day_l.length > 0)) {
                $('.show-avg-data').toggle(true);
                $('.show-no-avg-data').toggle(false);
                $('#total_l').html(data['total_l']);
                $('#total_m3').html(data['total_m3']);
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
            chart.series[0].setData(data['day_l']);
            chart.series[1].setData(data['day_m3']);

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
            text: "Consumo dos últimos 30 dias"
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
                var options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
                date = new Date(this.x).toLocaleDateString('pt-PT', options);
                text = "<strong>"+date+"</strong><br />"
                if(this.series.name == 'Litros') {
                    text += this.y + "l";
                }
                else if(this.series.name == 'Metros Cúbicos') {
                    text += this.y + "m³";
                }
                return text;
            }
        },
        xAxis: {
            type: 'datetime',
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
                name: 'Litros',
                data: []
            },
            {
                name: 'Metros Cúbicos',
                data: []
            },
        ]
    });
    chart.legend.group.hide();
    chart.legend.box.hide();
    chart.legend.display = false;
});