import React from "react";
import { Pie } from "react-chartjs-2";
import { MDBContainer } from "mdbreact";

class Chart extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataPie: {
              labels: this.props.topics.labels,
              datasets: [
                {
                  data: this.props.topics.data,
                  backgroundColor: [
                    "#F7464A",
                    "#46BFBD",
                    "#FDB45C",
                    "#949FB1",
                    "#4D5360",
                    "#AC64AD", 
                    "#F7464A",
                    "#46BFBD",
                    "#FDB45C",
                    "#949FB1",
                    "#4D5360",
                    "#AC64AD"
                  ],
                  hoverBackgroundColor: [
                    "#FF5A5E",
                    "#5AD3D1",
                    "#FFC870",
                    "#A8B3C5",
                    "#616774",
                    "#DA92DB", 
                    "#FF5A5E",
                    "#5AD3D1",
                    "#FFC870",
                    "#A8B3C5",
                    "#616774",
                    "#DA92DB"
                  ]
                }
              ]
            }
          }
    }

    componentDidUpdate(nextProps) {
        if(this.props !== nextProps) {
          this.setState({
            dataPie: {
                labels: this.props.topics.labels,
                datasets : [
                    {
                        data: this.props.topics.data,
                    }
                ]
            }
          });
        }
      }
    render() {
        return (
        <MDBContainer>
            <Pie data={this.state.dataPie} options={{ responsive: true }} />
        </MDBContainer>
        );
    }
}

export default Chart;