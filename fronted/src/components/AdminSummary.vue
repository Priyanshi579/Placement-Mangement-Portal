<template>
    <div>
        <h1 style = "text-align: center;">SUMMARY</h1>
        <h3 style = "text-align: center;">Total Users:{{ summary.total }} </h3>
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
    name:'AdminSummary',
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
                labels:['Company','Student','Active Students','Active Companies','Inactive Students','Inactive Companies','Pending Companies'],
                datasets:[{
                    label:'No of users',
                    data:[
                        this.summary.total_company,
                        this.summary.total_student,
                        this.summary.active_students,
                        this.summary.active_companies,
                        this.summary.inactive_students,
                        this.summary.inactive_companies,
                        this.summary.pending_companies
                        
                    ],
                    backgroundColor:'rgba(75,192,192,0.5)'
                }]
            }
        }
        
    },
    methods: {
        async fetchSummary(){
            try{
                const token = localStorage.getItem('admin_token')
                const response = await axios.get('http://localhost:5000/api/admin/summary',{
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