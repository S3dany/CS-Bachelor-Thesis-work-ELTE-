
         let data = [
      {
      id: 'Total amount',
      name: 'Amount',
      color: "#2a2a2a",
      value: total.toFixed(2)
    },
      {
      id: 'Local transactions',
      name: `(${((local_amount ) * 100 / total).toFixed(2)})% Local`,
      parent: 'Total amount',
      color: '#006700',
      value: local_amount.toFixed(2)
    }, {
      id: 'Foreign',
      name: `(${((total - (local_amount )) * 100 / total).toFixed(2)})% Foreign`,
      parent: 'Total amount',
      color: "#ff3232",
      value: (total - (local_amount )).toFixed(2)
    }];

         let data_2 = [
      {
      id: 'all transactions',
      name: 'No. Transactions',
      color: "#2a2a2a",
      value: no_all_transactions
    },
      {
      id: 'Local transactions',
      name: `(${((no_local_transactions ) * 100 / no_all_transactions).toFixed(2)})% Local`,
      parent: 'all transactions',
      color: '#006700',
      value: no_local_transactions
    }, {
      id: 'Foreign',
      name: `(${((no_all_transactions - (no_local_transactions )) * 100 / no_all_transactions).toFixed(2)})% Foreign`,
      parent: 'all transactions',
      color: "#ff3232",
      value: no_all_transactions - (no_local_transactions)
    },{
      id: 'complete',
      name: `(${(no_complete_transactions * 100 / no_all_transactions).toFixed(2)})% complete`,
      parent: 'Local transactions',
      color: "#004c00",
      value: no_complete_transactions
         },{
      id: 'partial',
      name: `(${(((no_local_transactions ) - no_complete_transactions) * 100 / no_all_transactions).toFixed(2)})% partial`,
      parent: 'Local transactions',
      color: "#00b200",
      value:(no_local_transactions ) - no_complete_transactions
         }];

         Highcharts.getOptions().colors.splice(0, 0, 'transparent');


    Highcharts.chart('amount', {

      chart: {
        height: '100%',
        backgroundColor: "transparent",
      },

      title: {
        text: 'Amounts analysis',
         style: {
            color: 'White',
            fontWeight: 'bold'
        }

      },
        subtitle: {
            text: "All percentages refer to ratio against the total value"
        },
      series: [{
        type: 'sunburst',
        data: data,
          name: "Value",
        allowDrillToNode: true,
        cursor: 'pointer',
        dataLabels: {
          format: '{point.name}',
          filter: {
            property: 'innerArcLength',
            operator: '>',
            value: 16
          },
          rotationMode: 'circular'
        },
        levels: [{
          level: 1,
          levelIsConstant: false,
          dataLabels: {
            filter: {
              property: 'outerArcLength',
              operator: '>',
              value: 64
            }
          }
        }, {
          level: 2,
          colorByPoint: true
        },
        {
          level: 3,
          colorVariation: {
            key: 'brightness',
            to: -0.5
          }
        }, {
          level: 4,
          colorVariation: {
            key: 'brightness',
            to: 0.5
          }
        }]

      }],
      tooltip: {
        headerFormat: '',
        pointFormat: '<b>{point.name}</b> is <b>{point.value}</b> USD'
      }
    });

    Highcharts.chart('no_of_transactions', {

      chart: {
        height: '100%',
        backgroundColor: "transparent",
      },

      title: {
        text: 'Number of transactions analysis',
          style: {
            color: 'White',
            fontWeight: 'bold'
        },

      },
        subtitle: {
            text: "All percentages refer to ratio against the total value"
        },
      series: [{
        type: 'sunburst',
        data: data_2,
          name: "Value",
        allowDrillToNode: true,
        cursor: 'pointer',
        dataLabels: {
          format: '{point.name}',
          filter: {
            property: 'innerArcLength',
            operator: '>',
            value: 16
          },
          rotationMode: 'circular'
        },
        levels: [{
          level: 1,
          levelIsConstant: false,
          dataLabels: {
            filter: {
              property: 'outerArcLength',
              operator: '>',
              value: 64
            }
          }
        }, {
          level: 2,
          colorByPoint: true
        },
        {
          level: 3,
          colorVariation: {
            key: 'brightness',
            to: -0.5
          }
        }, {
          level: 4,
          colorVariation: {
            key: 'brightness',
            to: 0.5
          }
        }]

      }],
      tooltip: {
        headerFormat: '',
        pointFormat: '<b>{point.name}</b> = <b>{point.value}</b>'
      }
    })
