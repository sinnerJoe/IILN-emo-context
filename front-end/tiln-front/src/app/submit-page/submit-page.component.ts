import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-submit-page',
  templateUrl: './submit-page.component.html',
  styleUrls: ['./submit-page.component.scss']
})
export class SubmitPageComponent implements OnInit {

  constructor(private http: HttpClient) { }
  firstReply = ""
  secondReply = ""
  thirdReply = ""
  response = null
  ngOnInit() {
  }


  sendData(){
    this.response = null
    this.http.post<any>("http://127.0.0.1:5000/emotion", {conversation: [this.firstReply, this.secondReply, this.thirdReply]}).subscribe(result => {
      console.log(result)
      if (result && result.emotion){
        this.response = result
      }

    })
  }
}
