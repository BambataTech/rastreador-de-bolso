import { Body, Controller, Get, Param, Post, Query } from '@nestjs/common';
import { Tweet } from './schemas/tweet.schema';
import { TweetsService } from './tweets.service';

@Controller('tweets')
export class TweetsController {
  constructor(private service: TweetsService) {}

  @Post('create')
  create(@Body() tweet: Tweet) {
    return this.service.create(tweet);
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return id;
  }

  @Get()
  async findMany(@Query() query) {
    return this.service.findAll(query);
  }
}
