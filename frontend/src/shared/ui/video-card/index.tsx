import { VideoCardProps } from './types'
import { 
    Card,
    CardBody,
    Text,
    Stack,
    Image,
} from 'shared/ui'
import { useNavigate } from 'react-router-dom'

export const VideoCard = ({
    id,
    name,
    date,
    url
}: VideoCardProps) => {
    const navigate = useNavigate()

    return (
        <Card
            size={'sm'}
            w={'100%'}
            h={'176px'}
            direction={'column'}
            overflow='hidden'
            borderRadius={'10px'}
            filter={'drop-shadow(0 2px 10px #FCFCFC)'}
            cursor={'pointer'}
            onClick={() => navigate(`/video/${id}`)}
        >
            <Image
                objectFit='cover'
                maxH={'70%'}
                src={url}
                alt={name}
            />
            <Stack>
                <CardBody p={'6px 16px'}>
                    <Text fontSize={'14px'} color={'gray.600'}>{name}</Text>
                    <Text fontSize={'12px'} color={'gray.600'}>{date}</Text>
                </CardBody>
            </Stack>
        </Card>
    )
}