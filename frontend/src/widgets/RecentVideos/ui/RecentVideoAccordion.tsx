import { useRecentVideos } from '../lib'
import {
    Grid,
    Box,
    Text,
    VideoCard,
    Accordion,
    AccordionItem,
    AccordionButton,
    AccordionIcon,
    AccordionPanel
} from 'shared/ui'
import { ChevronUp } from 'shared/iconpack'

function RecentVideoAccordion() {
    const data = useRecentVideos()

    return (
        <Accordion allowMultiple>
            <AccordionItem border={'none'}>
                <AccordionButton>
                    <Box as='span' flex='1' textAlign='left'>
                        <Text fontSize={'14px'} fontWeight={600}>Недавно обработанные</Text>
                    </Box>
                    <AccordionIcon as={ChevronUp} />
                </AccordionButton>
                <AccordionPanel pb={4}>
                {data && data.length != 0 ? (
                    <Grid 
                        templateColumns={'repeat(4, 1fr)'}
                        columnGap={'40px'}
                    >
                        {data.slice(0, 4).map((item) => (
                            <VideoCard
                                key={item.id}
                                id={item.id}
                                name={item.name}
                                date={item.created_at}
                                url={item.image_url}
                            />
                        ))}
                    </Grid>
                ) : (
                    <Text
                        fontSize={'14px'}
                        align={'center'}
                        mt={'20px'}
                    >
                        Здесь пока пусто
                    </Text>
                )}
                </AccordionPanel>
            </AccordionItem>
        </Accordion>
    )
}

export default RecentVideoAccordion
