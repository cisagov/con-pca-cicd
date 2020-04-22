import { Injectable, EventEmitter } from '@angular/core';

@Injectable()
export class LayoutMainService {
  static title: string;

  onTitleUpdate: EventEmitter<string> = new EventEmitter<string>();

  setTitle(title: string) {
    try {
        LayoutMainService.title = title;
    } catch { }

    this.onTitleUpdate.emit(LayoutMainService.title);
  }

  getTitle(){
      return LayoutMainService.title;
  }
}