<template>
    <div>
        <h1 style = "text-align: center;">List of Ongoing Company</h1>
        <div class = "table" style = "text-align: center;">
            <table border = "10px" bordlinecolor="white">
                <thead>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Description</th>
                </thead>
                <tbody>
                    <tr v-for = "company in company_details" :key = "company.id">
                        <td>{{company.name}} </td>
                        <td>{{company.email}} </td>
                        <td>{{company.contact}} </td>
                        <td>{{company.description}} </td>
                        <td><td> <button class="btn btn-success"  @click = "approved_company(company.id)">Approve</button></td></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    
</template>
<script>
import axios from 'axios'
export default{
    name:'AdminCompany',
    data(){
        return{
            company_details:[]
        }
    },
    methods:{
        async fetchcompanydetails(){
            const token = localStorage.getItem('admin_token');
            const res = await axios.get('http://localhost:5000/api/get/unapproved/company',{
                headers:{
                    Authorization: `Bearer ${token}`
                }
            });
            this.company_details = res.data
            
        },
        async approved_company(id){
            const token = localStorage.getItem('admin_token')
            const res = await axios.put(`http://localhost:5000/api/approval/company/${id}`,{},{
                headers:{
                    Authorization:`Bearer ${token}`
                }
            })
            this.company_details = this.company_details.filter(company => company.id !==  id)
            alert("company is Approved successful")
        }
        

    },
    mounted(){
        this.fetchcompanydetails()
    }
}
</script>

<style scoped>
    .table{
        border:2px none;
        margin-top:10px;
        width:715px;
        /* ADD THESE THREE LINES TO CENTER THE CANVAS: */
        display: flex;
        justify-content: center; /* Centers horizontally */
        align-items: flex-start; /* Keeps the canvas layout sticking towards the top */
        /* min-height: 100vh; */
    }
</style>
