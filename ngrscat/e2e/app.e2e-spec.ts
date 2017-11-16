import { NgrscatPage } from './app.po';

describe('ngrscat App', function() {
  let page: NgrscatPage;

  beforeEach(() => {
    page = new NgrscatPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
