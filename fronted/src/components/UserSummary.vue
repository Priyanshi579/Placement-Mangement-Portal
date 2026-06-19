<template>
    <div>
        <h1 style = "text-align: center;">USER  APPLICATION SUMMARY</h1>
        <h3 style = "text-align: center;">Total Applications: {{summary.total_application}}</h3>
        <Bar :data="countChartsData"  :options="{responsive: true}"/>
    </div>
</template>
<script>
import axios from 'axios'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)
export default{
    name:'UserSummary',
    components:{
        Bar,
    },
    data(){
        return{
            summary:[],
        }
    },
    computed: {
        countChartsData(){
            return{
                labels:[ 'Applied','Selected','Waiting','Rejected'],
                datasets:[{
                    label:'No of applications',
                    data:[
                        this.summary.apply,
                        this.summary.selected,
                        this.summary.waiting,
                        this.summary.rejected
                    ],
                    backgroundColor:'rgba(75,192,192,0.5)'
                }]
            }
        }
        
    },
    methods: {
        async fetchSummary(){
            try{
                const token = localStorage.getItem('token')
                const response = await axios.get('http://localhost:5000/user/summary',{
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });
                console.log(response.data)
                this.summary = response.data
            }catch(error){
                console.log(error)
            }
            
        }
        
        
    },
    mounted(){
        this.fetchSummary()
    }
}
</script>