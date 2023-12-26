export interface Video {
    id: number;
    name: string;
    description: string;
    url: string;
    createdAt: Date;
    updatedAt: Date;
    likes: number;
    views: number;
    userId: number;
    comments: Comment[];
    isLiked: boolean;
    isDisliked: boolean;
    isSaved: boolean;
    image: string;
    thumbnail: string;

  }